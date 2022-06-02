---
id: how-to-install-bloomberg
title: Installing Bloomberg
sidebar_label: Installing Bloomberg
slug: /how-to-install-bloomberg
---
:::warning

This only works on Windows

:::

### [Source](https://medium.com/@johann_78792/getting-started-with-bloombergs-python-desktop-api-5fd083b4193a)
1) Download Bloomberg Professional

● https://www.bloomberg.com/professional/support/software-updates/

● Select “Bloomberg Terminal — New/Upgrade Installation”
2) Install Bloomberg

● Go to location where installable was downloaded. Typically, the default is “C:\Users\your_name\Downloads”

● Double click and follow steps through installation wizard

● Make sure to install to C:\blp

● This is the default path and do not alter it. This will become important in step 7

3) Activate your licence

● Speak to your Bloomberg Sales Rep about this process. Beyond the scope of this post.

4) Download and install Visual Studio Build Tools 2017

● The python desktop api (blpapi) requires an installation of the C++ Library SDK

● This means that you will need a C++ compiler

● https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=BuildTools&rel=15

● Run install manager and follow steps until you get to selecting workloads. Make below selections:

● C++/CLI Support and VC++ 2015.3 v14.00 (v140) toolset for desktop are the key components here

● Select “Install”

● Carry on with other steps below as this may take a while to download and install

● Be sure to check process is complete before starting step 7

● You do not need to sign in to, create account or start Visual Studio to complete blpapi setup

● Restart PC

5) Download and Unzip BloombergWindowsSDK

● Log into Bloomberg Terminal

● WAPI \<GO\>

● Select “API Download Center” under Express Links

● Select download for “B-Pipe, Server API, Desktop API and Platform SDKs” i.e. first download button

● In your Downloads folder you will see

● Extract to C:\blp

● C:\blp before and after unzipping

6) Overwrite .dll files

● Make sure to exit Bloomberg Terminal before doing the following

● Go to C:\blp\BloombergWindowsSDK\C++API\v3.12.3.1\bin

● Copy blpapi3_32.dll and blpapi3_64.dll

● Go to C:\blp\DAPI

● Paste .dll files and overwrite the ones that were there

7) Install python blpapi (Compile C++ SDK Library)

● Make sure step 4 is completed before continuing

● Some guides set PATH variable. This is not necessary as the correct PATH variable was set during installation of Bloomberg Terminal

● Into prompt copy and run to install blpapi: python -m pip install — index-url=https://bloomberg.bintray.com/pip/simple blpapi

8) Test if blpapi correctly installed

● Using command line: python import blapi

● If no error message returned then library was imported which means that it was installed correctly