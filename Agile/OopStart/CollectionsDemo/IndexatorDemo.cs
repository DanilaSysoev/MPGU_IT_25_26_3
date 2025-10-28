namespace CollectionsDemo;

public class IndexatorDemo
{
    public int this[int index]
    {
        get
        {
            if (next is null)
                return random.Next(100);

            var res = next.Value;
            next = null;
            return res;
        }
        set
        {
            next = value;
        }
    }

    public int this[int i1, int i2] => i1 * i2;

    private int? next = null;
    private readonly Random random = new Random();
}
