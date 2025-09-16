namespace Inheritance;

public class Rectangle : GeometricFigure
{
    public double Width { get; set; }
    public double Height { get; set; }

    public Rectangle(Point center, double width, double height)
        : base(center)
    {
        Width = width;
        Height = height;
    }

    public new double Length()
    {
        return 2 * (Width + Height);
    }

    public override string ToString()
    {
        return $"Rectangle: Center = {Center}, " +
               $"Width = {Width}, Height = {Height}";
    }
}