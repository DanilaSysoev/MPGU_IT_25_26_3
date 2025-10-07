namespace EnumsAndCollections.DamageSystem;

public class PiercingDamage : Damage
{
    public PiercingDamage(int value) : base(value)
    {}

    public override void ApplyTo(Fighter fighter)
    {
        base.ApplyTo(fighter);
        fighter.Debuff = Debuff.Bleedeeng;
    }
}
