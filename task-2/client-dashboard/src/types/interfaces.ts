export interface TimeSeriesDataPoint {
    average_wind_speed: number;
    average_power: number;
    average_azimuth: number;
    average_external_temperature: number;
    average_internal_temperature: number;
    average_rpm: number;
}


export interface QueryParameters {
    turbine_id?: string;
    start_date?: string;
    end_date?: string;
}
