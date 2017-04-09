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
.module main.exe // GUID = {DF18CF73-CD54-44D4-BE71-D6C4243EBC79}


  .class private auto ansi beforefieldinit hello
  	extends [mscorlib]System.Object
  {
    .field  public  int32[] a

    // method line 1
    .method public hidebysig specialname rtspecialname 
           instance default void '.ctor' ()  cil managed 
    {
        // Method begins at RVA 0x2050
	// Code size 20 (0x14)
	.maxstack 8
	IL_0000:  ldarg.0 
	IL_0001:  ldc.i4.s 0x0a
	IL_0003:  newarr [mscorlib]System.Int32
	IL_0008:  stfld int32[] hello::a
	IL_000d:  ldarg.0 
	IL_000e:  call instance void object::'.ctor'()
	IL_0013:  ret 
    } // end of method hello::.ctor

  } // end of class hello

  .class private auto ansi beforefieldinit MainClass
  	extends [mscorlib]System.Object
  {

    // method line 2
    .method public hidebysig specialname rtspecialname 
           instance default void '.ctor' ()  cil managed 
    {
        // Method begins at RVA 0x2065
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
        // Method begins at RVA 0x206d
	.entrypoint
	// Code size 1 (0x1)
	.maxstack 8
	IL_0000:  ret 
    } // end of method MainClass::Main

  } // end of class MainClass

