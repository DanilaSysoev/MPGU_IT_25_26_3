using Testable;

namespace MyTests;

public class SquareEquationSolverTests
{
    private SquareEquationSolver simple_solver;
    private SquareEquationSolver solver_2r;
    private SquareEquationSolver solver_1r;
    private SquareEquationSolver solver_0r;

    [SetUp]
    public void Setup()
    {
        simple_solver = new SquareEquationSolver(10, 1, -3);
        solver_2r = new SquareEquationSolver(1, 1, -2);
        solver_1r = new SquareEquationSolver(1, 2, 1);
        solver_0r = new SquareEquationSolver(1, 2, 2);
    }

    [Test]
    public void Solved_CreateNewSolver_IsFalse()
    {
        Assert.That(simple_solver.Solved, Is.False);
    }

    [Test]
    public void Solved_CreateNewSolverThenSolve_IsTrue()
    {
        simple_solver.Solve();
        Assert.That(simple_solver.Solved, Is.True);
    }

    [Test]
    public void Solved_CallsolveTwice_IsAgainTrue()
    {
        simple_solver.Solve();
        simple_solver.Solve();
        Assert.That(simple_solver.Solved, Is.True);
    }

    [Test]
    public void Solve_SolveTwoRootsEquation_LengthIs2()
    {
        solver_2r.Solve();
        Assert.That(solver_2r.Roots.Length, Is.EqualTo(2));
    }

    [Test]
    public void Solve_SolveTwoRootsEquation_RootsIsCorrect()
    {
        solver_2r.Solve();
        var roots = new List<double>(solver_2r.Roots);
        roots.Sort();
        Assert.That(roots[0], Is.EqualTo(-2).Within(0.000001));
        Assert.That(roots[1], Is.EqualTo(1).Within(0.000001));
    }

    [Test]
    public void Solve_SolveOneRootsEquation_LengthIs1()
    {
        solver_1r.Solve();
        Assert.That(solver_1r.Roots.Length, Is.EqualTo(1));
    }

    [Test]
    public void Solve_SolveOneRootsEquation_RootsIsCorrect()
    {
        solver_1r.Solve();
        var roots = new List<double>(solver_1r.Roots);
        roots.Sort();
        Assert.That(roots[0], Is.EqualTo(-1).Within(0.000001));
    }

    [Test]
    public void Solve_SolveZeroRootsEquation_LengthIs0()
    {
        solver_0r.Solve();
        Assert.That(solver_0r.Roots.Length, Is.EqualTo(0));
    }

    [Test]
    public void Roots_SolveIsNotCalled_ThrowsException()
    {
        Assert.That(
            () => simple_solver.Roots,
            Throws.InvalidOperationException
                  .With
                  .Message                  
                  .Contain("it is impossible to get roots without calling soleve()")
                  .IgnoreCase
        );
    }
}
