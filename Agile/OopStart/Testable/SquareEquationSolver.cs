namespace Testable;

public class SquareEquationSolver
{
    public bool Solved { get; private set; }
    public double[] Roots
    {
        get
        {
            if (!Solved)
            {
                throw new InvalidOperationException(
                    "It is impossible to get roots without calling Soleve()"
                );
            }
            return roots!;
        }
        private set => roots = value;
    }

    public SquareEquationSolver(double a, double b, double c)
    {
        Solved = false;

        this.a = a;
        this.b = b;
        this.c = c;
    }

    public void Solve()
    {
        if (Solved)
            return;

        double d = b * b - 4 * a * c;
        if (d > 0)
        {
            Roots = [
                (-b + Math.Sqrt(d)) / (2 * a),
                (-b - Math.Sqrt(d)) / (2 * a)
            ];
        }
        else if (Math.Abs(d) < 0.000001)
        {
            Roots = [
                -b / (2 * a),
            ];
        }
        else
        {
            Roots = [];
        }

        Solved = true;
    }

    private readonly double a;
    private readonly double b;
    private readonly double c;
    private double[]? roots;
}
