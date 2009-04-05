/** 
 * @file llfloateravatarinfo.cpp
 * @author McCabe Maxsted
 * @brief LLFloaterAvatarInfo class implementation
 * Avatar information as shown in a floating browser window.
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
 * online at http://secondlifegrid.net/programs/open_source/licensing/gplv2
 * 
 * There are special exceptions to the terms and conditions of the GPL as
 * it is applied to this Source Code. View the full text of the exception
 * in the file doc/FLOSS-exception.txt in this software distribution, or
 * online at http://secondlifegrid.net/programs/open_source/licensing/flossexception
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

#include "llfloateravatarinfo.h"

// Viewer libs
#include "llviewercontrol.h"
#include "llwebbrowserctrl.h"
#include "llalertdialog.h"
#include "llagentdata.h"
#include "lluuid.h"

// Linden libs
#include "lluictrlfactory.h"

// Globals
LLMap< const LLUUID, LLFloaterAvatarInfo* > gAvatarInfoInstances;

///----------------------------------------------------------------------------
/// Class LLFloaterAvatarInfo
///----------------------------------------------------------------------------

// Default constructor
LLFloaterAvatarInfo::LLFloaterAvatarInfo(const LLUUID &avatar_id)
:	LLFloater(std::string("avatarinfo")),
	mWebBrowser(0),
	mAvatarID(avatar_id)
{
	// Create floater from its XML definition
	LLUICtrlFactory::getInstance()->buildFloater(this, "floater_profile.xml");
	
	// Remember the one instance
	//sInstance = this;

	std::ostringstream id;
	id << mAvatarID;

	std::string profile_url = "";
	profile_url = getString("real_url") + id.str();	

	mWebBrowser = getChild<LLWebBrowserCtrl>("floater_profile_browser" );
	if (mWebBrowser)
	{
		// Open links in internal browser
		mWebBrowser->setOpenInExternalBrowser(false);

		// This is a "chrome" floater, so we don't want anything to
		// take focus
		mWebBrowser->setTakeFocusOnClick(false);

		mWebBrowser->navigateTo(profile_url);
	}

	gAvatarInfoInstances.addData(mAvatarID, this);
}

// Destructor
LLFloaterAvatarInfo::~LLFloaterAvatarInfo()
{
	// Save floater position
	gSavedSettings.setRect("FloaterProfileRect", getRect() );

	gAvatarInfoInstances.removeData(mAvatarID);
}

// Show the profile
LLFloaterAvatarInfo* LLFloaterAvatarInfo::show(const LLUUID &avatar_id)
{
	if (avatar_id.isNull())
	{
		return NULL;
	}

	LLFloaterAvatarInfo *floater;

	if (gAvatarInfoInstances.checkData(avatar_id))
	{
		// ...bring that window to front
		floater = gAvatarInfoInstances.getData(avatar_id);
		floater->open();
	}
	else
	{
		floater =  new LLFloaterAvatarInfo(avatar_id);

		LLRect rect = gSavedSettings.getRect("FloaterProfileRect");
		floater->reshape(rect.getWidth(), rect.getHeight());
		floater->setRect(rect);

		std::string profile_base_url = floater->getString("real_url");

		// do not build the floater if there the url is empty
		if (profile_base_url.empty())
		{
			llwarns << "Cannot open! Profile url could not be found!" << llendl;
			return NULL;
		}
		else
		{
			floater->center();
			floater->open();
		}
	}
	return floater;
}
	
// These are the 'Profile' buttons in the UI
// static
void LLFloaterAvatarInfo::showFromObject(const LLUUID& avatar_id, std::string tab_name)
{
	show(avatar_id);
}


// static
void LLFloaterAvatarInfo::showFromDirectory(const LLUUID &avatar_id)
{
	show(avatar_id);
}

// static
void LLFloaterAvatarInfo::showFromFriend(const LLUUID& agent_id, BOOL online)
{
	show(agent_id);
}

// static
void LLFloaterAvatarInfo::showFromProfile(const LLUUID &avatar_id, LLRect rect)
{
	show(avatar_id);
}

// Save our visibility state on close in case the user accidentally
// quit the application while the tutorial was visible.
// virtual
void LLFloaterAvatarInfo::onClose(bool app_quitting)
{
	destroy();
}
