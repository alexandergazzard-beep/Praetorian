"""Player movement profiles for BP_WreckagePlayer_Runtime (pure data; no Unreal imports).

Shared by the gameplay builder (editor Python), the live tuning script and the movement tests.
Units are Unreal centimetres/seconds. Halo-derived numbers are approximations from labelled
community measurements scaled to this character's body; they are not official Halo values.
"""

PLAYER_BP = '/Game/WreckagePrototype/Blueprints/BP_WreckagePlayer_Runtime.BP_WreckagePlayer_Runtime'
ACTIVE_PROFILE = 'reach'  # User chose Halo: Reach as the priority reference on 2026-10-08.
LOOK_SENSITIVITY_DEFAULT = 0.6  # Original hard-coded mouse multiplier, now a variable.

# Fields captured before/after tuning. Unchanged fields are recorded to prove they stayed put.
MOVEMENT_FIELDS = ['MaxWalkSpeed', 'MaxWalkSpeedCrouched', 'MaxAcceleration', 'BrakingDecelerationWalking',
                   'GroundFriction', 'BrakingFrictionFactor', 'bUseSeparateBrakingFriction', 'JumpZVelocity',
                   'GravityScale', 'AirControl', 'AirControlBoostMultiplier', 'AirControlBoostVelocityThreshold',
                   'FallingLateralFriction', 'BrakingDecelerationFalling', 'MaxStepHeight', 'WalkableFloorAngle',
                   'CrouchedHalfHeight', 'bCanWalkOffLedges', 'bCanWalkOffLedgesWhenCrouching',
                   'PerchRadiusThreshold', 'bApplyGravityWhileJumping', 'NavAgentProps']
CAPSULE_FIELDS = ['CapsuleHalfHeight', 'CapsuleRadius']

# --- Reference measurements (community, Bungie.net forum post by "mdenni", 2011-10-08) ---
# Speed from Forge grid squares; jump = standing foot to head-top at apex in 1/100 Spartan heights.
REFERENCE = {
    'reach': {'run_m_s': 6.82, 'apex_head_spartan_heights': 1.95, 'airtime_s': 1.2},
    'halo3': {'run_m_s': 7.69, 'apex_head_spartan_heights': 2.45, 'airtime_s': 1.4},
}
SPARTAN_HEIGHT_CM = 213.4   # ~7 ft player height documented in Halo editing-kit player metrics (assumption for scaling).
BODY_HEIGHT_CM = 176.0      # This project's standing capsule (2 x 88 cm half-height); unchanged by tuning.
UE_GRAVITY = 980.0          # Project default world gravity magnitude (cm/s^2).


def derived(name):
    """Body-relative conversion of one reference: speed in body heights/s, jump in body heights."""
    ref = REFERENCE[name]
    scale = BODY_HEIGHT_CM / SPARTAN_HEIGHT_CM
    run = ref['run_m_s'] * 100.0 * scale
    clearance = (ref['apex_head_spartan_heights'] - 1.0) * BODY_HEIGHT_CM
    airtime = ref['airtime_s']
    gravity = 8.0 * clearance / airtime ** 2          # symmetric ballistic arc: h = g T^2 / 8
    return {'run': run, 'clearance': clearance, 'airtime': airtime, 'gravity': gravity,
            'jump_z': gravity * airtime / 2.0, 'gravity_scale': gravity / UE_GRAVITY}


def _profile(name):
    d = derived(name)
    run = round(d['run'])
    return {
        'MaxWalkSpeed': float(run),
        # No reliable Halo crouch measurement: keep the original crouch:run ratio (220/450).
        'MaxWalkSpeedCrouched': float(round(run * 220.0 / 450.0)),
        # Estimates for hands-on review (no published Halo data): ~0.15 s to full speed.
        'MaxAcceleration': float(round(run / 0.15, -1)),
        'JumpZVelocity': round(d['jump_z'], 1),
        'GravityScale': round(d['gravity_scale'], 4),
        # Estimate: strong arcade air steering; unchanged momentum when no input (braking 0).
        'AirControl': 0.3,
    }


PROFILES = {
    # Values read from the saved Blueprint before tuning (see reports/movement_original_settings.json).
    'original': {'MaxWalkSpeed': 450.0, 'MaxWalkSpeedCrouched': 220.0, 'MaxAcceleration': 2048.0,
                 'JumpZVelocity': 450.0, 'GravityScale': 1.2, 'AirControl': 0.05},
    'reach': _profile('reach'),
    # Documented alternative only; not applied (exit gate height would need a coordinated map change).
    'halo3': _profile('halo3'),
}


if __name__ == '__main__':
    import json
    print(json.dumps({'derived': {k: derived(k) for k in REFERENCE}, 'profiles': PROFILES}, indent=2))
