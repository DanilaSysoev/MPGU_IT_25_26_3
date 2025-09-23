using System;

namespace Abstraction;

public abstract class GeometricFigure
{
    public abstract string Name { get; }

    public abstract double Square();
    public abstract double Length();
}
