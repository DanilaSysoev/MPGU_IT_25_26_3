using System;

namespace EnumsAndCollections;

public class Entity : ItemBase, IElement, IWidget
{
    public void OwnMethod()
    {
        Console.WriteLine("Own impl");
    }

    public void SomeMethod()
    {
        Console.WriteLine("Some concrete impl");
    }
}
