.assembly extern mscorlib
{
  .ver 4:0:0:0
  .publickeytoken = (B7 7A 5C 56 19 34 E0 89 ) // .z\V.4..
}
.assembly 'main'
{
  .custom instance void class [mscorlib]System.Runtime.CompilerServices.RuntimeCompatibilityAttribute::'.ctor'() =  (
		01 00 01 00 54 02 16 57 72 61 70 4E 6F 6E 45 78   // ....T..WrapNonEx
		63 65 70 74 69 6F 6E 54 68 72 6F 77 73 01       ) // ceptionThrows.

  .hash algorithm 0x00008004
  .ver  0:0:0:0
}
.module main.exe // GUID = {8A747AEE-9A49-4158-881F-07BEAD00A3DB}


  .class private auto ansi beforefieldinit MainClass
  	extends [mscorlib]System.Object
  {
    .field  public static  int32 x
    .field  public static  int32 y
    .field  public static  int32 z
    .field  private static  bool b1

    // method line 1
    .method public hidebysig specialname rtspecialname 
           instance default void '.ctor' ()  cil managed 
    {
        // Method begins at RVA 0x2050
	// Code size 7 (0x7)
	.maxstack 8
	IL_0000:  ldarg.0 
	IL_0001:  call instance void object::'.ctor'()
	IL_0006:  ret 
    } // end of method MainClass::.ctor

    // method line 2
    .method private static hidebysig 
           default void Main (string[] args)  cil managed 
    {
        // Method begins at RVA 0x2058
	.entrypoint
	// Code size 45 (0x2d)
	.maxstack 2
	.locals init (
		bool	V_0,
		int32	V_1)
	IL_0000:  ldc.i4.1 
	IL_0001:  stsfld int32 MainClass::x
	IL_0006:  ldc.i4.2 
	IL_0007:  stsfld int32 MainClass::y
	IL_000c:  ldsfld int32 MainClass::x
	IL_0011:  ldsfld int32 MainClass::y
	IL_0016:  add 
	IL_0017:  stsfld int32 MainClass::z
	IL_001c:  ldc.i4.1 
	IL_001d:  stsfld bool MainClass::b1
	IL_0022:  ldstr "Hello World"
	IL_0027:  call void class [mscorlib]System.Console::WriteLine(string)
	IL_002c:  ret 
    } // end of method MainClass::Main

  } // end of class MainClass

