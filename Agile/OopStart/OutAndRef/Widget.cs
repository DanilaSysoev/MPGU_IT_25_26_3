namespace OutAndRef;

public static class Widget
{
    public static void SomeMethod(Parameter parameter)
    {
        parameter.Name = "Updated name";
        parameter.Value = 10;

        // parameter = new Parameter
        // {
        //     Name = "Updated name",
        //     Value = 10
        // };
    }

    public static void SomeRefMethod(ref Parameter parameter)
    {
        parameter = new Parameter
        {
            Name = "Updated ref name",
            Value = 20
        };
    }

    public static void SomeOutMethod(out Parameter parameter)
    {
        parameter = new Parameter
        {
            Name = "Updated out name",
            Value = 30
        };
    }
}
