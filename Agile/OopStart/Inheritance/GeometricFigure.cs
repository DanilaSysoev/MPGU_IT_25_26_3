namespace Inheritance;

public class GeometricFigure
{
    public Point Center { get; set; }

    public GeometricFigure(Point center)
    {
        Center = center;
    }

    public double Length()
    {
        return 0;
    }

    public void Move(Point motion)
    {
        Center = new Point(Center.x + motion.x, Center.y + motion.y);
    }

    public override string ToString()
    {
        return $"GeometricFigure: Center = {Center}";
    }
}