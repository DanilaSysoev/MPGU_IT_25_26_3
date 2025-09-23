using System;

namespace Abstraction;

public class FigureObserver
{
    public void PrintInfo(GeometricFigure figure)
    {
        Console.WriteLine(
            $"Фигура: {figure.Name}, Площадь: {figure.Square()}, Длина: {figure.Length()}"
        );
    }
}
