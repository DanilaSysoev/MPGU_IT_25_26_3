namespace ExceptionsDemo;


public class MyOwnException : Exception
{
    public MyOwnException(string message) : base(message)
    { }

    public MyOwnException(
        string message, Exception innerException
    ) : base(message, innerException)
    { }
}
