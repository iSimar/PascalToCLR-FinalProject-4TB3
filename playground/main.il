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
		ldc.i4.1
		stsfld int32 MainClass::x
		ret
	}
}

