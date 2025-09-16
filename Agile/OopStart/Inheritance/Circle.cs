namespace Inheritance;

public class Circle : GeometricFigure
{
    public double Radius { get; set; }

    public Circle(Point center, double radius) : base(center)
    {
        Radius = radius;
    }

    public new double Length()
    {
        return 2 * Math.PI * Radius;
    }

    public override string ToString()
    {
        return $"Circle: Center = {Center}, Radius = {Radius}";
    }
}
