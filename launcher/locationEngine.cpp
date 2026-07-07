#define INITGUID // This forces MinGW to define the GUIDs locally instead of looking for them in -luuid
#include <windows.h>
#include <shlobj.h>
#include <shlwapi.h>
#include <iostream>
#include <string>
#include <algorithm>
#include <cwctype>

// Helper for case-insensitive search
bool ContainsIgnoreCase(const std::wstring& str, const std::wstring& search) {
    auto it = std::search(
        str.begin(), str.end(),
        search.begin(), search.end(),
        [](wchar_t ch1, wchar_t ch2) { return std::towlower(ch1) == std::towlower(ch2); }
    );
    return it != str.end();
}

void FindApplication(std::wstring targetName) {
    HRESULT hr = CoInitializeEx(NULL, COINIT_APARTMENTTHREADED | COINIT_DISABLE_OLE1DDE);
    if (FAILED(hr)) return;

    IShellFolder* pDesktop = NULL;
    hr = SHGetDesktopFolder(&pDesktop);
    if (SUCCEEDED(hr)) {
        PIDLIST_ABSOLUTE pidlAppsFolder;
        hr = SHParseDisplayName(L"shell:AppsFolder", NULL, &pidlAppsFolder, 0, NULL);
        if (SUCCEEDED(hr)) {
            IShellFolder* pAppsFolder = NULL;
            hr = pDesktop->BindToObject(pidlAppsFolder, NULL, IID_IShellFolder, (void**)&pAppsFolder);
            
            if (SUCCEEDED(hr)) {
                IEnumIDList* pEnum = NULL;
                hr = pAppsFolder->EnumObjects(NULL, SHCONTF_FOLDERS | SHCONTF_NONFOLDERS, &pEnum);
                
                if (SUCCEEDED(hr)) {
                    PITEMID_CHILD pidlItem = NULL;
                    ULONG fetched;
                    bool found = false;

                    while (pEnum->Next(1, &pidlItem, &fetched) == S_OK && !found) {
                        STRRET strRetName;
                        if (SUCCEEDED(pAppsFolder->GetDisplayNameOf(pidlItem, SHGDN_NORMAL, &strRetName))) {
                            wchar_t* pszName = nullptr;
                            StrRetToStrW(&strRetName, pidlItem, &pszName);
                            
                            if (pszName && ContainsIgnoreCase(pszName, targetName)) {
                                STRRET strRetPath;
                                if (SUCCEEDED(pAppsFolder->GetDisplayNameOf(pidlItem, SHGDN_FORPARSING, &strRetPath))) {
                                    wchar_t* pszPath = nullptr;
                                    StrRetToStrW(&strRetPath, pidlItem, &pszPath);
                                    
                                    std::wcout << L"Found App: " << pszName << std::endl;
                                    std::wcout << L"Path/ID:   " << pszPath << std::endl;
                                    
                                    CoTaskMemFree(pszPath);
                                    found = true;
                                }
                            }
                            CoTaskMemFree(pszName);
                        }
                        CoTaskMemFree(pidlItem);
                    }
                    if (!found) {
                        std::wcout << L"Application not found." << std::endl;
                    }
                    pEnum->Release();
                }
                pAppsFolder->Release();
            }
            CoTaskMemFree(pidlAppsFolder);
        }
        pDesktop->Release();
    }
    CoUninitialize();
}

int wmain(int argc, wchar_t* argv[]) {
    if (argc < 2) {
        std::wcout << L"Usage: search.exe <AppName>" << std::endl;
        return 1;
    }
    FindApplication(argv[1]);
    return 0;
}

int main(int argc, char* argv[]) {
    int argc_w;
    wchar_t** argv_w = CommandLineToArgvW(GetCommandLineW(), &argc_w);
    if (argv_w == NULL) return 1;
    int result = wmain(argc_w, argv_w);
    LocalFree(argv_w);
    return result;
}