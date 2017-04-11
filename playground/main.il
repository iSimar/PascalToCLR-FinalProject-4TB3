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
.module main.exe // GUID = {0A225ECB-2B14-4E7C-B9EF-C587133DDE7C}


  .class private auto ansi beforefieldinit MainClass
  	extends [mscorlib]System.Object
  {
    .field  private static  bool t
    .field  private static  bool b
    .field  private static  int32 x
    .field  private static  int32 y

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
	// Code size 63 (0x3f)
	.maxstack 8
	IL_0000:  ldc.i4.1 
	IL_0001:  stsfld bool MainClass::t
	IL_0006:  ldsfld int32 MainClass::x
	IL_000b:  ldsfld int32 MainClass::y
	IL_0010:  bgt IL_001c

	IL_0015:  ldsfld bool MainClass::t
	IL_001a:  br.s IL_001d

	IL_001c:  ldc.i4.1 
	IL_001d:  stsfld bool MainClass::b
	IL_0022:  ldsfld bool MainClass::b
	IL_0027:  brfalse IL_0037

	IL_002c:  ldc.i4.7 
	IL_002d:  call void class [mscorlib]System.Console::Write(int32)
	IL_0032:  br IL_003e

	IL_0037:  ldc.i4.s 0x09
	IL_0039:  call void class [mscorlib]System.Console::Write(int32)
	IL_003e:  ret 
    } // end of method MainClass::Main

  } // end of class MainClass

