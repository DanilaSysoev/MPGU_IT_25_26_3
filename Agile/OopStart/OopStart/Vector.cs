class Vector
{
    // private float x;
    // private float y;

    private double angle;

    // public double R
    // {
    //     get { return r; }
    //     set { r = value; }
    // }

    public double R { get; init; } = 10;

    public double X
    {
        get { return R * Math.Cos(angle); }
    }
    public double Y
    {
        get { return R * Math.Sin(angle); }
    }

    public Vector(float x, float y)
    {
        R = Math.Sqrt(x * x + y * y);
        angle = Math.Atan2(y, x);
    }
}
