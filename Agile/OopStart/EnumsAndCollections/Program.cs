using EnumsAndCollections;

static class Program
{
    public static void Main()
    {
        Entity entity = new Entity();
        SomeStaticMethod(entity);

        entity.DoSomething();
        entity.OwnMethod();
        entity.SomeMethod();

        ((IElement)entity).SomeOtherMethod();

        EnumUsage(MyEnum.First);
    }

    public static void SomeStaticMethod(IElement element)
    {
        element.SomeOtherMethod();
    }

    public static void EnumUsage(MyEnum e)
    {
        Console.WriteLine((int)e);
        Console.WriteLine((MyEnum)1);

        Console.WriteLine(Enum.Parse<MyEnum>("First"));
        foreach (var ev in Enum.GetValues<MyEnum>())
            Console.WriteLine(ev);
        Console.WriteLine(Enum.GetName(e));
    }
}
