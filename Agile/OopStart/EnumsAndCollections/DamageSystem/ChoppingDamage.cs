namespace EnumsAndCollections.DamageSystem;

public class ChoppingDamage : Damage
{
    public ChoppingDamage(int value) : base(value)
    { }

    public override void ApplyTo(Fighter fighter)
    {
        base.ApplyTo(fighter);
        fighter.Debuff = Debuff.Injury;
    }
}
