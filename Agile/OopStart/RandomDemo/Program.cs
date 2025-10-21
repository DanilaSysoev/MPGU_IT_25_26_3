Random random = new Random(10);

Console.WriteLine(random.Next());
Console.WriteLine(random.Next(100));
Console.WriteLine(random.Next(10, 15));

Console.WriteLine(random.NextDouble());
Console.WriteLine(random.NextDouble() * 10 + 10); // double [10, 20]
