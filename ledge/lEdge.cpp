// lEdge.cpp : this is used to overcome the error massage from
// ms windows if for some reason we cannot open edge or ie.
// ((boo hooo->automating windows is a bitch
//

#include "stdafx.h"

wchar_t* charToWChar(char* text)
{
	size_t size = strlen(text) + 1;
	wchar_t* wa = new wchar_t[size];
	mbstowcs(wa, text, size);
	return wa;
}

void main(int argc, char* argv[])
{
	//auto lpparam = charToWChar(argv[2]);
	if (argc < 2) {
		return;
	}
	__try {
		ShellExecuteA(
			NULL,
			"open",
			argv[1],
			NULL,
			NULL,
			SW_SHOW
		);
	}
	__except (-1) {
		return;
	}
}

