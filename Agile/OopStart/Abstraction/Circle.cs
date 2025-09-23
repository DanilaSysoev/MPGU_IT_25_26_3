using System;

namespace Abstraction;

public class Circle : GeometricFigure
{
    public override string Name => "Circle";
    public double Radius { get; init; }

    public Circle(double radius)
    {
        Radius = radius;
    }

    public override double Length()
    {
        return 2 * Math.PI * Radius;
    }

    public override double Square()
    {
        return Math.PI * Radius * Radius;
    }
}
