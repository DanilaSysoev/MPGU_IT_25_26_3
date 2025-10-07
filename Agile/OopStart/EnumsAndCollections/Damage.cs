namespace EnumsAndCollections.DamageSystem;

public class Damage
{
    public int Value { get; init; }

    public Damage(int value)
    {
        Value = value;
    }

    public virtual void ApplyTo(Fighter fighter)
    {
        fighter.Hp = Math.Max(0, fighter.Hp - Value);
    }
}

