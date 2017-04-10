.assembly extern mscorlib{}
.assembly 'main'{}


.class private auto ansi beforefieldinit a
	extends [mscorlib]System.Object
{
	.field  public int32[] arr
	.method public hidebysig specialname rtspecialname
		instance default void '.ctor' ()  cil managed 
	{
		.maxstack 8
		ldarg.0
		ldc.i4.s 0x8
		newarr [mscorlib]System.Int32
		stfld int32[] a::arr
		ldarg.0
		call instance void object::'.ctor'()
		ret
	}
}
.class private auto ansi beforefieldinit r
	extends [mscorlib]System.Object
{
	.field  public int32 f
	.field  public class a g
	.field  public int32 h
	.method public hidebysig specialname rtspecialname
		instance default void '.ctor' ()  cil managed 
	{
		.maxstack 8
		ldarg.0
		newobj instance void class a::'.ctor'()
		stfld class a r::g
		ldarg.0
		call instance void object::'.ctor'()
		ret
	}
}


.class private auto ansi beforefieldinit MainClass
	extends [mscorlib]System.Object
{
	.field static class a v
	.field static class r w
	.field static int32 x
	

	.class nested private auto ansi beforefieldinit q
		extends [mscorlib]System.Object
	{
		.method public static hidebysig
			default void main_proc (class a c, class r d)  cil managed
		{
			.locals init (
				int32 V_0)
			ldc.i4.3
			stloc.0
			ldarg.1
			ldfld int32 r::h
			call void class [mscorlib]System.Console::Write(int32)
			ldarg.0
			ldfld int32[] a::arr
			ldc.i4.1
			ldelem.i4
			call void class [mscorlib]System.Console::Write(int32)
			ldarg.1
			ldfld class a r::g
			ldfld int32[] a::arr
			ldloc.0
			ldelem.i4
			call void class [mscorlib]System.Console::Write(int32)
			call void class [mscorlib]System.Console::WriteLine()
			ldarg.0
			ldfld int32[] a::arr
			ldc.i4.7
			ldc.i4.7
			stelem.i4
			ldarg.0
			ldfld int32[] a::arr
			ldloc.0
			ldc.i4.4
			add
			ldelem.i4
			call void class [mscorlib]System.Console::Write(int32)
			ldarg.1
			ldfld class a r::g
			ldfld int32[] a::arr
			ldloc.0
			ldc.i4.2
			mul
			ldc.i4.7
			stelem.i4
			ldarg.1
			ldfld class a r::g
			ldfld int32[] a::arr
			ldc.i4.6
			ldelem.i4
			call void class [mscorlib]System.Console::Write(int32)
			ret
		}
	}
	

	.method private static hidebysig default void Main (string[] args)
		cil managed
	{
		.entrypoint
		ldc.i4.s 0x9
		stsfld int32 MainClass::x
		ldsfld class r MainClass::w
		ldc.i4.5
		stfld int32 r::h
		ldsfld class r MainClass::w
		ldfld int32 r::h
		call void class [mscorlib]System.Console::Write(int32)
		ldsfld class a MainClass::v
		ldfld int32[] a::arr
		ldc.i4.1
		ldc.i4.3
		stelem.i4
		ldsfld class a MainClass::v
		ldfld int32[] a::arr
		ldsfld int32 MainClass::x
		ldc.i4.8
		sub
		ldelem.i4
		call void class [mscorlib]System.Console::Write(int32)
		ldsfld class r MainClass::w
		ldfld class a r::g
		ldfld int32[] a::arr
		ldsfld int32 MainClass::x
		ldc.i4.3
		div
		ldc.i4.s 0x9
		stelem.i4
		ldsfld class r MainClass::w
		ldfld class a r::g
		ldfld int32[] a::arr
		ldc.i4.3
		ldelem.i4
		call void class [mscorlib]System.Console::Write(int32)
		call void class [mscorlib]System.Console::WriteLine()
		ldsfld class a MainClass::v
		ldsfld class r MainClass::w
		call void class MainClass/q::main_proc(class a, class r)
		call void class [mscorlib]System.Console::WriteLine()
		ldsfld class a MainClass::v
		ldfld int32[] a::arr
		ldc.i4.7
		ldelem.i4
		call void class [mscorlib]System.Console::Write(int32)
		ldsfld class r MainClass::w
		ldfld class a r::g
		ldfld int32[] a::arr
		ldc.i4.6
		ldelem.i4
		call void class [mscorlib]System.Console::Write(int32)
		ret
	}
	.method private static hidebysig specialname rtspecialname
		default void '.cctor' ()  cil managed 
	{
		.maxstack 8
		newobj instance void class a::'.ctor'()
		stsfld class a MainClass::v
		newobj instance void class r::'.ctor'()
		stsfld class r MainClass::w
		ret
	}
}