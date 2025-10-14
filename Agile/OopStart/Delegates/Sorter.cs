namespace Delegates;

public delegate int ComparerDelegate(int lo, int ro);

public class Sorter
{
    public ComparerDelegate Comparer { get; set; }
    public int[] Sorted
    {
        get
        {
            if (!sorted)
                Sort();
            return CopyTarget();
        }
    }

    public Sorter(int[] target, ComparerDelegate comparer)
    {
        this.target = target;
        this.Comparer = comparer;
        this.sorted = false;
    }

    public void Sort()
    {
        sorted = true;

        for (int ready = 0; ready < target.Length - 1; ready++)
        {
            for (int cur = 1; cur < target.Length - ready; cur++)
            {
                if (Comparer(target[cur - 1], target[cur]) > 0)
                {
                    (target[cur - 1], target[cur]) =
                        (target[cur], target[cur - 1]);
                }
            }
        }
    }


    private readonly int[] target;
    private bool sorted;

    private int[] CopyTarget()
    {
        var res = new int[target.Length];
        Array.Copy(target, res, target.Length);
        return res;
    }
}
