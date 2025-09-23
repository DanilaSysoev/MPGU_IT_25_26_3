using System;

namespace Abstraction;

public class Rectangle : GeometricFigure
{
    public override string Name => "Rectangle";
    public double Height { get; init; }
    public double Width { get; init; }

    public Rectangle(double height, double width)
    {
        Height = height;
        Width = width;
    }

    public override double Length()
    {
        return 2 * (Height + Width);
    }

    public override double Square()
    {
        return Height * Width;
    }
}
