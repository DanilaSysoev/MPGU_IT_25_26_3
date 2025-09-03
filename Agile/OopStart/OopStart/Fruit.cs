class Fruit
{
    public string Name { get; init; }
    public string Color { get; private set; }
    public string Gustus { get; private set; }

    public Fruit(string name, string color, string gustus)
    {
        Name = name;
        Color = color;
        Gustus = gustus;
    }

    public void Maturus()
    {
        Console.WriteLine($"{Name} is mature.");
    }

    public override string ToString()
    {
        return $"{Name} is {Color} and {Gustus}.";
    }
}