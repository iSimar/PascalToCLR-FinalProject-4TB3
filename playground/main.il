.assembly extern mscorlib{}
.assembly 'main'{}


.class private auto ansi beforefieldinit MainClass
	extends [mscorlib]System.Object
{
	.field static int32 x
	.method private static hidebysig default void Main (string[] args)
		cil managed
	{
		.entrypoint
		.locals init (int32 V_0)
		call string class [mscorlib]System.Console::ReadLine()
		call int32 class [mscorlib]System.Convert::ToInt32(string)
		stsfld int32 MainClass::x
		ldsfld int32 MainClass::x
		ldc.i4.3
		mul
		stsfld int32 MainClass::x
		ldsfld int32 MainClass::x
		call void class [mscorlib]System.Console::Write(int32)
		call void class [mscorlib]System.Console::WriteLine()
		call void class [mscorlib]System.Console::WriteLine()
		ldsfld int32 MainClass::x
		ldc.i4.5
		mul
		call void class [mscorlib]System.Console::Write(int32)
		ret
	}
}