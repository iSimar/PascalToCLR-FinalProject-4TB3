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
.module main.exe // GUID = {6C190334-B89A-4F94-8F0D-10CB9DE1E3B3}


  .class private auto ansi beforefieldinit l
  	extends [mscorlib]System.Object
  {
    .field  public  int32 i

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
    } // end of method l::.ctor

  } // end of class l

  .class private auto ansi beforefieldinit MainClass
  	extends [mscorlib]System.Object
  {
    .field  public static  class l y

    // method line 2
    .method public hidebysig specialname rtspecialname 
           instance default void '.ctor' ()  cil managed 
    {
        // Method begins at RVA 0x2058
	// Code size 7 (0x7)
	.maxstack 8
	IL_0000:  ldarg.0 
	IL_0001:  call instance void object::'.ctor'()
	IL_0006:  ret 
    } // end of method MainClass::.ctor

    // method line 3
    .method private static hidebysig 
           default void Main (string[] args)  cil managed 
    {
        // Method begins at RVA 0x2060
	.entrypoint
	// Code size 27 (0x1b)
	.maxstack 8
	IL_0000:  ldsfld class l MainClass::y
	IL_0005:  ldc.i4.4 
	IL_0006:  stfld int32 l::i
	IL_000b:  ldsfld class l MainClass::y
	IL_0010:  ldfld int32 l::i
	IL_0015:  call void class [mscorlib]System.Console::Write(int32)
	IL_001a:  ret 
    } // end of method MainClass::Main

  } // end of class MainClass

