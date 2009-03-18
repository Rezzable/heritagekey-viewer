/** 
 * @file llviewernetwork.h
 * @author James Cook
 * @brief Networking constants and globals for viewer.
 *
 * $LicenseInfo:firstyear=2006&license=viewergpl$
 * 
 * Copyright (c) 2006-2008, Linden Research, Inc.
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

#ifndef LL_LLVIEWERNETWORK_H
#define LL_LLVIEWERNETWORK_H

class LLHost;

enum EGridInfo
{
	GRID_INFO_NONE,
	GRID_INFO_HERITAGE_KEY,
	GRID_INFO_AGNI,
	GRID_INFO_ADITI,
	GRID_INFO_LOCAL,
	GRID_INFO_OTHER, // IP address set via command line option
	GRID_INFO_COUNT
};

/**
 * @brief A class to manage the viewer's login state.
 * 
 **/
class LLViewerLogin : public LLSingleton<LLViewerLogin>
{
public:
	LLViewerLogin();

	void setGridChoice(EGridInfo grid);
	void setGridChoice(const std::string& grid_name);
	void resetURIs();

	/**
	* @brief Get the enumeration of the grid choice.
	* Should only return values > 0 && < GRID_INFO_COUNT
	**/
	EGridInfo getGridChoice() const;

	/**
	* @brief Get a readable label for the grid choice.
	* Returns the readable name for the grid choice. 
	* If the grid is 'other', returns something
	* the string used to specifiy the grid.
	**/
	std::string getGridLabel() const; 

  /**
   * @brief Get the code name for the grid choice.
   *
   * Returns the code name for the grid choice, as designated
   * by Linden Lab. The SL main grid is Agni, and the beta
   * grid is Aditi. There are other LL testing grids with code
   * names, but we don't care about those.
   *
   * This string is used primarily for fetching the proper
   * login splash page, since the web server expects "Agni"
   * and "Aditi", not "SL Main Grid" and "SL Beta Grid".
   */
	std::string getGridCodeName() const; 

	std::string getKnownGridLabel(EGridInfo grid_index) const; 

	void getLoginURIs(std::vector<std::string>& uris) const;
	std::string getHelperURI() const;

	bool isInProductionGrid();

private:
	EGridInfo mGridChoice;
	std::string mGridName;
};

const S32 MAC_ADDRESS_BYTES = 6;
extern unsigned char gMACAddress[MAC_ADDRESS_BYTES];		/* Flawfinder: ignore */

#endif
