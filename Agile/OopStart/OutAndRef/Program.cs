using OutAndRef;

Parameter p1 = new Parameter
{
    Name = "Initial name",
    Value = 5
};
Parameter p2 = p1;

Widget.SomeMethod(p1);
Console.WriteLine(p1);
Console.WriteLine(p2);

Widget.SomeRefMethod(ref p1);
Console.WriteLine(p1);
Console.WriteLine(p2);

Widget.SomeOutMethod(out p2);
Console.WriteLine(p1);
Console.WriteLine(p2);
