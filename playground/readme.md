C# to exe to CIL (store in file)
mcs main2.cs && monodis main.exe > main.il


CIL to exe
ilasm main.il /output:main.exe

run exe
mono main.exe




mcs main.cs && monodis main.exe > main.il && rm main.exe

ilasm main.il /output:main.exe && mono main.exe && rm main.exe