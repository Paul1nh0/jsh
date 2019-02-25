// lEdge.cpp : this is used to overcome the error massage from
// ms windows if for some reason we cannot open edge or ie.
// ((boo hooo->automating windows is a bitch
//

#include "stdafx.h"

void main(int argc, char* argv[])
{

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

