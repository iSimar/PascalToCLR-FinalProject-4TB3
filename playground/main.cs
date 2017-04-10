using System;

class a{
    public int[] arr = new int[7];
}
class r{
    public int f;
    public a g = new a();
    public int h;
}
class MainClass
{
    public static a v = new a();
    public static r w = new r();
    public static int x;
    
    class q{
        public static void main_proc(a c, r d){
            int y;
            y = 3;
            Console.Write(d.h);
            Console.Write(c.arr[1]);
            Console.Write(d.g.arr[y]);
            Console.WriteLine();
            c.arr[6]=7;
        }
    }
    static void Main(string[] args)
    {
        x = 9;
        w.g.arr[x/3] = 9;
        q.main_proc(v, w);
    }
}