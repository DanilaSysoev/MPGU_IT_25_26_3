using System;

namespace Abstraction;

public class Printer
{
    public void Print(Parent entity)
    {
        entity.PrintInfo();
    }
}
