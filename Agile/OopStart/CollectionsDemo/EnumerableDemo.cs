using System.Collections;

namespace CollectionsDemo;

public class EnumerableDemo : IEnumerable<int>
{
    private readonly List<int> data;

    public EnumerableDemo(int[] data) => this.data = [.. data];

    public IEnumerator<int> GetEnumerator()
    {
        return data.GetEnumerator();
    }

    IEnumerator IEnumerable.GetEnumerator()
    {
        return data.GetEnumerator();
    }
}
