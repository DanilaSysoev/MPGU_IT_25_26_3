namespace EnumsAndCollections;

public class Damage
{
    public int Value { get; init; }

    public virtual void ApplyTo(Fighter fighter)
    {
        fighter.Hp = Math.Max(0, fighter.Hp - Value);
    }
}
