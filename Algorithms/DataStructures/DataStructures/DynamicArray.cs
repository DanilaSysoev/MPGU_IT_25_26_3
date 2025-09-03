namespace DataStructures;

public class DynamicArray<T>
{
    public DynamicArray()
    {
        data = new T[DefaultCapacity];
        size = 0;
        capacity = DefaultCapacity;
    }

    public void PushBack(T value)
    {
        throw new NotImplementedException(); // <-- Remove this line
    }

    public void PopBack()
    { 
        throw new NotImplementedException(); // <-- Remove this line
    }

    public void Insert(int index, T value)
    {
        throw new NotImplementedException(); // <-- Remove this line
    }

    public void Remove(int index)
    {
        throw new NotImplementedException(); // <-- Remove this line
    }

    public int Size
    {
        get
        {
            throw new NotImplementedException(); // <-- Remove this line
        }
    }

    public T this[int index]
    {
        get
        {
            throw new NotImplementedException(); // <-- Remove this line
        }
        set
        {
            throw new NotImplementedException(); // <-- Remove this line
        }
    }


    private void ThrowError(int index)
    {
        throw new IndexOutOfRangeException(
            $"Index {index} is out of range. Size equals to {size}."
        );
    }

    private T[] data;
    private int size;
    private int capacity;

    private const int DefaultCapacity = 32;
}
