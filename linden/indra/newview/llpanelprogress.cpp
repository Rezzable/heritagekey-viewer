/**
 * @file llpanelprogress.cpp
 * @brief LLPanelProgress class implementation
 *
 * $LicenseInfo:firstyear=2002&license=viewergpl$
 *
 * Copyright (c) 2002-2007, Linden Research, Inc.
 *
 * Second Life Viewer Source Code
 * The source code in this file ("Source Code") is provided by Linden Lab
 * to you under the terms of the GNU General Public License, version 2.0
 * ("GPL"), unless you have obtained a separate licensing agreement
 * ("Other License"), formally executed by you and Linden Lab.  Terms of
 * the GPL can be found in doc/GPL-license.txt in this distribution, or
 * online at http://secondlife.com/developers/opensource/gplv2
 *
 * There are special exceptions to the terms and conditions of the GPL as
 * it is applied to this Source Code. View the full text of the exception
 * in the file doc/FLOSS-exception.txt in this software distribution, or
 * online at http://secondlife.com/developers/opensource/flossexception
 *
 * By copying, modifying or distributing this software, you acknowledge
 * that you have read and understood your obligations described above,
 * and agree to abide by those obligations.
 *
 * ALL LINDEN LAB SOURCE CODE IS PROVIDED "AS IS." LINDEN LAB MAKES NO
 * WARRANTIES, EXPRESS, IMPLIED OR OTHERWISE, REGARDING ITS ACCURACY,
 * COMPLETENESS OR PERFORMANCE.
 * $/LicenseInfo$
 */

#include "llviewerprecompiledheaders.h"

#include "llpanelprogress.h"

#include "indra_constants.h"
#include "llmath.h"
#include "llgl.h"
#include "llui.h"
#include "lluictrlfactory.h"
#include "llfontgl.h"
#include "llimagegl.h"
#include "lltimer.h"
#include "llglheaders.h"

#include "llagent.h"
#include "llappviewer.h"
#include "llbutton.h"
#include "llprogressbar.h"
#include "lltextbox.h"
#include "llfocusmgr.h"
#include "llstartup.h"
#include "lluictrlfactory.h"
#include "llviewercontrol.h"
#include "llviewerimagelist.h"
#include "llviewerwindow.h"
#include "llwebbrowserctrl.h"

LLPanelProgress* LLPanelProgress::sInstance = NULL;

S32 gStartImageWidth = 1;
S32 gStartImageHeight = 1;
const F32 FADE_IN_TIME = 1.f;

const std::string ANIMATION_FILENAME = "Login Sequence ";
const std::string ANIMATION_SUFFIX = ".jpg";
const F32 TOTAL_LOGIN_TIME = 10.f;	// seconds, wild guess at time from GL context to actual world view
S32 gLastStartAnimationFrame = 0;	// human-style indexing, first image = 1
const S32 ANIMATION_FRAMES = 1; //13;

// XUI:translate
LLPanelProgress::LLPanelProgress(const std::string& name, const LLRect &rect)
: LLPanel(name, rect, FALSE)
{
	mDrawBackground = TRUE;

	LLUICtrlFactory::getInstance()->buildPanel(this, "panel_progress.xml");
	setRect(rect);
	reshape(rect.getWidth(), rect.getHeight());

	setPercent(0.f);

	LLButton* cancel = getChild<LLButton>("cancel_btn");
	if (cancel)
	{
		childSetAction("cancel_btn", onCancelButtonClicked, this);
	}

	mFadeTimer.stop();
	setVisible(FALSE);

	sInstance = this;
}


LLPanelProgress::~LLPanelProgress()
{
	gFocusMgr.releaseFocusIfNeeded( this );

	sInstance = NULL;
}

BOOL LLPanelProgress::handleHover(S32 x, S32 y, MASK mask)
{
	if( childrenHandleHover( x, y, mask ) == NULL )
	{
		lldebugst(LLERR_USER_INPUT) << "hover handled by LLPanelProgress" << llendl;
		gViewerWindow->setCursor(UI_CURSOR_WAIT);
	}
	return TRUE;
}

BOOL LLPanelProgress::handleKeyHere(KEY key, MASK mask, BOOL called_from_parent)
{
	if( getVisible() )
	{
		// Suck up all keystokes except CTRL-Q.
		if( ('Q' == key) && (MASK_CONTROL == mask) )
		{
			LLAppViewer::instance()->userQuit();
		}
		return TRUE;
	}
	return FALSE;
}

void LLPanelProgress::setVisible(BOOL visible)
{
	LLWebBrowserCtrl* browser = getChild<LLWebBrowserCtrl>("browser");
	browser->addObserver(this);
	browser->navigateTo("http://google.com");
	sendChildToFront(browser);

	if (getVisible() && !visible)
	{
		mFadeTimer.start();
	}
	else if (!getVisible() && visible)
	{
		gFocusMgr.setTopCtrl(this);
		mFadeTimer.stop();
		LLPanel::setVisible(visible);
	}
}


void LLPanelProgress::draw()
{
	if (gNoRender)
	{
		return;
	}

	S32 width  = gViewerWindow->getWindowWidth();
	S32 height = gViewerWindow->getWindowHeight();

	// Make sure the progress view always fills the entire window.
	reshape( width, height );

	// Paint bitmap if we've got one
	if (mDrawBackground)
	{
		glPushMatrix();
		if (gStartImageGL)
		{
			LLGLSUIDefault gls_ui;
			gGL.getTexUnit(0)->bind(gStartImageGL);
			glColor4f(1.f, 1.f, 1.f, mFadeTimer.getStarted() ? clamp_rescale(mFadeTimer.getElapsedTimeF32(), 0.f, FADE_IN_TIME, 1.f, 0.f) : 1.f);
			F32 image_aspect = (F32)gStartImageWidth / (F32)gStartImageHeight;
			F32 view_aspect = (F32)width / (F32)height;
			// stretch image to maintain aspect ratio
			if (image_aspect > view_aspect)
			{
				glTranslatef(-0.5f * (image_aspect / view_aspect - 1.f) * width, 0.f, 0.f);
				glScalef(image_aspect / view_aspect, 1.f, 1.f);
			}
			else
			{
				glTranslatef(0.f, -0.5f * (view_aspect / image_aspect - 1.f) * height, 0.f);
				glScalef(1.f, view_aspect / image_aspect, 1.f);
			}
			gl_rect_2d_simple_tex( getRect().getWidth(), getRect().getHeight() );
			gGL.getTexUnit(0)->unbind(LLTexUnit::TT_TEXTURE);
		}
		else
		{
			gGL.getTexUnit(0)->unbind(LLTexUnit::TT_TEXTURE);
			glColor4f(0.f, 0.f, 0.f, 1.f);
			gl_rect_2d(getRect());
		}
		glPopMatrix();
	}

	if (mFadeTimer.getStarted())
	{
		LLPanel::draw();
		if (mFadeTimer.getElapsedTimeF32() > FADE_IN_TIME)
		{
			gFocusMgr.removeTopCtrlWithoutCallback(this);
			LLPanel::setVisible(FALSE);
			gStartImageGL = NULL;
		}
		return;
	}

	// draw children
	LLPanel::draw();
}

void LLPanelProgress::setText(const std::string& text)
{
	LLTextBox* status = getChild<LLTextBox>("status");
	if (status)
	{
		status->setText(text);
	}
}

void LLPanelProgress::setPercent(const F32 percent)
{
	LLProgressBar* progress = getChild<LLProgressBar>("progress_bar");
	if (progress)
	{
		progress->setPercent( llclamp(percent, 0.f, 100.f) );
	}
}

void LLPanelProgress::setMessage(const std::string& msg)
{
	LLTextBox* message = getChild<LLTextBox>("message");
	if (message)
	{
		message->setText(msg);
	}
}

void LLPanelProgress::setCancelButtonVisible(BOOL b, const std::string& label)
{
	LLButton* cancel = getChild<LLButton>("cancel_btn");
	if (cancel)
	{
		cancel->setVisible( b );
		cancel->setEnabled( b );
		cancel->setLabelSelected(label);
		cancel->setLabelUnselected(label);
	}
}

// static
void LLPanelProgress::onCancelButtonClicked(void*)
{
	if (gAgent.getTeleportState() == LLAgent::TELEPORT_NONE)
	{
		LLAppViewer::instance()->requestQuit();
	}
	else
	{
		gAgent.teleportCancel();
		sInstance->childDisable("cancel_btn");
		sInstance->setVisible(FALSE);
	}
}
