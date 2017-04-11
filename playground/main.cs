using System;

class MainClass
{

    static Boolean t;
    static Boolean b;
    static int x;
    static int y;
    static void Main(string[] args)
    {
        t = true;
        b = (x > y) || t;   
        if(b){
            Console.Write(7);
        }
        else{
            Console.Write(9);
        }
    }
}