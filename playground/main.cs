using System;
class MainClass
{
    public static int x;
    static void Main(string[] args)
    {
        x = Convert.ToInt32(Console.ReadLine());
        x = 3*x;
        Console.Write(x);
        Console.WriteLine();
        Console.WriteLine(x*5);
    }
}