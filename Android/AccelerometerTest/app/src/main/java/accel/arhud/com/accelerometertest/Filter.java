package accel.arhud.com.accelerometertest;

/**
 * Created by david on 07/03/18.
 */

/**
 * A discrete-time filter for raw sensor values.
 */
public interface Filter {
    /**
     * Update filter with the latest value.
     *
     * @return latest filtered value.
     */
    float push(float value);

    /**
     * Reset filter to the given value.
     */
    void reset(float value);

    /**
     * @return latest filtered value.
     */
    float get();
}