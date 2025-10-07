namespace EnumsAndCollections.DamageSystem;

public class CrushingDamage : Damage
{
    public CrushingDamage(int value) : base(value)
    { }

    public override void ApplyTo(Fighter fighter)
    {
        base.ApplyTo(fighter);
        fighter.Debuff = Debuff.Stun;
    }
}
