/**
 * @file llprogressbar.cpp
 * @brief LLProgressBar class implementation
 *
 * $LicenseInfo:firstyear=2002&license=viewergpl$
 *
 * Copyright (c) 2002-2008, Linden Research, Inc.
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

#include "linden_common.h"

#include "llprogressbar.h"

#include "indra_constants.h"
#include "llmath.h"
#include "llgl.h"
#include "llui.h"
#include "llfontgl.h"
#include "llimagegl.h"
#include "lltimer.h"
#include "llglheaders.h"

#include "llfocusmgr.h"

static LLRegisterWidget<LLProgressBar> r("progress_bar");

LLProgressBar::LLProgressBar(const std::string& name, const LLRect &rect) 
	: LLView(name, rect, FALSE),
	  mImageBar( NULL ),
	  mImageShadow( NULL )
{
	mPercentDone = 0.f;

	// Defaults:

	setImageBar("rounded_square.tga");
	setImageShadow("rounded_square_soft.tga");

	mColorBackground = LLColor4(0.3254f, 0.4000f, 0.5058f, 1.0f);
	mColorBar        = LLColor4(0.5764f, 0.6627f, 0.8352f, 1.0f);
	mColorBar2       = LLColor4(0.5764f, 0.6627f, 0.8352f, 1.0f);
	mColorShadow     = LLColor4(0.2000f, 0.2000f, 0.4000f, 1.0f);
}

LLProgressBar::~LLProgressBar()
{
	gFocusMgr.releaseFocusIfNeeded( this );
}

void LLProgressBar::draw()
{
	static LLTimer timer;

	if ( !getVisible() )
	{
		return;
	}

	//reshape(mRect.getWidth(), mRect.getHeight(), TRUE);

	//S32 bar_bottom = mRect.mBottom;
	//S32 bar_left   = mRect.mLeft;
	S32 bar_height = getRect().getHeight();
	S32 bar_width  = getRect().getWidth();

	gl_draw_scaled_image_with_border(
		2, -2,
		16, 16,
		bar_width,
		bar_height,
		mImageShadow,
		mColorShadow);

	gl_draw_scaled_image_with_border(
		0, 0,
		16, 16,
		bar_width,
		bar_height,
		mImageBar,
		mColorBar2);


	// "Pulsing" effect, these next two layers fade in and out across time.
	F32 alpha = 0.5f + 0.5f*0.5f*(1.f + (F32)sin(3.f*timer.getElapsedTimeF32()));

	LLColor4 bg_color = mColorBackground;
	bg_color.mV[3] = bg_color.mV[3]*alpha;

	gl_draw_scaled_image_with_border(
	  2, 2,
	  16, 16,
	  bar_width - 4,
	  bar_height - 4,
	  mImageBar,
	  bg_color);

	LLColor4 bar_color = mColorBar;
	bar_color.mV[3] = bar_color.mV[3]*alpha;

	gl_draw_scaled_image_with_border(
	  2, 2,
	  16, 16,
	  llround((bar_width - 4) * (mPercentDone / 100.f)),
	  bar_height - 4,
	  mImageBar,
	  bar_color);

}

void LLProgressBar::setPercent(const F32 percent)
{
	mPercentDone = llclamp(percent, 0.f, 100.f);
}

void LLProgressBar::setImageBar( const std::string &bar_name )
{
	mImageBar = LLUI::sImageProvider->getUIImage(bar_name)->getImage();
	///setImageBarID(LLUI::findAssetUUIDByName(bar_name));
	//mImageBarName = bar_name;
}

//void LLProgressBar::setImageBarID(const LLUUID &bar_id)
//{
//	//mImageBarName = "";
//	mImageBar = LLUI::sImageProvider->getUIImageByID(bar_id);
//}

void LLProgressBar::setImageShadow(const std::string &shadow_name)
{
	mImageShadow = mImageShadow = LLUI::sImageProvider->getUIImage(shadow_name)->getImage();
	///setImageShadowID(LLUI::findAssetUUIDByName(shadow_name));
	//mImageShadowName = shadow_name;
}

//void LLProgressBar::setImageShadowID(const LLUUID &shadow_id)
//{
//	//mImageShadowName = "";
//	mImageShadow = LLUI::sImageProvider->getUIImageByID(shadow_id);
//}


void LLProgressBar::setColorBar(const LLColor4 &c)
{
	mColorBar = c;
}
void LLProgressBar::setColorBar2(const LLColor4 &c)
{
	mColorBar2 = c;
}
void LLProgressBar::setColorShadow(const LLColor4 &c)
{
	mColorShadow = c;
}
void LLProgressBar::setColorBackground(const LLColor4 &c)
{
	mColorBackground = c;
}


// static
LLView* LLProgressBar::fromXML(LLXMLNodePtr node, LLView *parent, LLUICtrlFactory *factory)
{
	std::string name("progress_bar");
	node->getAttributeString("name", name);

	LLProgressBar *progress = new LLProgressBar(name, LLRect());


	std::string image_bar;
	if (node->hasAttribute("image_bar")) node->getAttributeString("image_bar",image_bar);
	if (image_bar != LLStringUtil::null) progress->setImageBar(image_bar);


	std::string image_shadow;
	if (node->hasAttribute("image_shadow")) node->getAttributeString("image_shadow",image_shadow);
	if (image_shadow != LLStringUtil::null) progress->setImageShadow(image_shadow);


	LLColor4 color_bar;
	if (node->hasAttribute("color_bar"))
	{
		node->getAttributeColor4("color_bar",color_bar);
		progress->setColorBar(color_bar);
	}


	LLColor4 color_bar2;
	if (node->hasAttribute("color_bar2"))
	{
		node->getAttributeColor4("color_bar2",color_bar2);
		progress->setColorBar2(color_bar2);
	}


	LLColor4 color_shadow;
	if (node->hasAttribute("color_shadow"))
	{
		node->getAttributeColor4("color_shadow",color_shadow);
		progress->setColorShadow(color_shadow);
	}


	LLColor4 color_bg;
	if (node->hasAttribute("color_bg"))
	{
		node->getAttributeColor4("color_bg",color_bg);
		progress->setColorBackground(color_bg);
	}


	progress->initFromXML(node, parent);

	return progress;
}
