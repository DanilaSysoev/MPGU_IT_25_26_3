using System;

namespace Abstraction;

public class StaticPoly
{
    public StaticPoly()
    {
        iField = 0;
        fField = 0;
    }
    public StaticPoly(int i, float f)
    {
        iField = i;
        fField = f;
    }

    public void Print()
    {
        Console.WriteLine($"iField = {iField}, fField = {fField}");
    }
    public void Print(int times)
    {
        for(int i = 0; i < times; i++)
        {
            Print();
        }
    }

    private int iField;
    private float fField;
}
