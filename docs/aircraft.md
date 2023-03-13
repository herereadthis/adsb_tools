# aircraft.json

<!-- https://www.adsbexchange.com/ads-b-data-field-explanations/ -->


<table border="0" style="border-width: 0">
    <tbody>
        <tr>
            <td>hex</td>
            <td colspan="2">the 24-bit ICAO identifier of the aircraft, as 6 hex digits. The identifier may start with '~', this means that the address is a non-ICAO address (e.g. from TIS-B).</td>
        </tr>
        <tr>
            <td rowspan="9">type</td>
            <td colspan="2">type of underlying message, one of:
</td>
        </tr>
        <tr>
            <td>adsb_icao</td>
            <td>messages from a Mode S or ADS-B transponder, using a 24-bit ICAO address</td>
        </tr>
        <tr>
            <td>adsb_icao_nt</td>
            <td>messages from an ADS-B equipped "non-transponder" emitter e.g. a ground vehicle, using a 24-bit ICAO address</td>
        </tr>
        <tr>
            <td>adsr_icao</td>
            <td>rebroadcast of ADS-B messages originally sent via another data link e.g. UAT, using a 24-bit ICAO address</td>
        </tr>
        <tr>
            <td>tisb_icao</td>
            <td>traffic information about a non-ADS-B target identified by a 24-bit ICAO address, e.g. a Mode S target tracked by secondary radar</td>
        </tr>
        <tr>
            <td>adsb_other</td>
            <td>messages from an ADS-B transponder using a non-ICAO address, e.g. anonymized address</td>
        </tr>
        <tr>
            <td>adsr_other</td>
            <td>rebroadcast of ADS-B messages originally sent via another data link e.g. UAT, using a non-ICAO address</td>
        </tr>
        <tr>
            <td>tisb_other</td>
            <td>traffic information about a non-ADS-B target using a non-ICAO address</td>
        </tr>
        <tr>
            <td>tisb_trackfile</td>
            <td>traffic information about a non-ADS-B target using a track/file identifier, typically from primary or Mode A/C radar</td>
        </tr>
        <tr>
            <td>flight</td>
            <td colspan=2>callsign, the flight name or aircraft registration as 8 chars (2.2.8.2.6)</td>
        </tr>
        <tr>
            <td>alt_baro</td>
            <td colspan=2>the aircraft barometric altitude in feet</td>
        </tr>
        <tr>
            <td>alt_geom</td>
            <td colspan=2>geometric (GNSS / INS) altitude in feet referenced to the WGS84 ellipsoid</td>
        </tr>
        <tr>
            <td>gs</td>
            <td colspan=2>ground speed in knots</td>
        </tr>
        <tr>
            <td>ias</td>
            <td colspan=2>indicated air speed in knots</td>
        </tr>
        <tr>
            <td>tas</td>
            <td colspan=2>true air speed in knots</td>
        </tr>
        <tr>
            <td>mach</td>
            <td colspan=2>Mach number</td>
        </tr>
        <tr>
            <td>track</td>
            <td colspan=2>true track over ground in degrees (0-359)</td>
        </tr>
        <tr>
            <td>track_rate</td>
            <td colspan=2>Rate of change of track, degrees/second</td>
        </tr>
        <tr>
            <td>roll</td>
            <td colspan=2>Roll, degrees, negative is left roll</td>
        </tr>
        <tr>
            <td>mag_heading</td>
            <td colspan=2>Heading, degrees clockwise from magnetic north</td>
        </tr>
        <tr>
            <td>true_heading</td>
            <td colspan=2>Heading, degrees clockwise from true north</td>
        </tr>
        <tr>
            <td>baro_rate</td>
            <td colspan=2>Rate of change of barometric altitude, feet/minute</td>
        </tr>
        <tr>
            <td>geom_rate</td>
            <td colspan=2>Rate of change of geometric (GNSS / INS) altitude, feet/minute</td>
        </tr>
        <tr>
            <td>squawk</td>
            <td colspan=2>Mode A code (Squawk), encoded as 4 octal digits</td>
        </tr>
        <tr>
            <td>emergency</td>
            <td colspan="2">ADS-B emergency/priority status, a superset of the 7x00 squawks (2.2.3.2.7.8.1.1)</td>
        </tr>
        <tr>
            <td>category</td>
            <td colspan=2>emitter category to identify particular aircraft or vehicle classes (values A0 - D7) (2.2.3.2.5.2)</td>
        </tr>
        <tr>
            <td>nav_qnh</td>
            <td colspan=2>altimeter setting (QFE or QNH/QNE), hPa</td>
        </tr>
        <tr>
            <td>nav_altitude_mcp</td>
            <td colspan=2>selected altitude from the Mode Control Panel / Flight Control Unit (MCP/FCU) or equivalent equipment</td>
        </tr>
        <tr>
            <td>nav_altitude_fms</td>
            <td colspan=2>selected altitude from the Flight Manaagement System (FMS) (2.2.3.2.7.1.3.3</td>
        </tr>
        <tr>
            <td>nav_heading</td>
            <td colspan=2>selected heading (True or Magnetic is not defined in DO-260B, mostly Magnetic as that is the de facto standard) (2.2.3.2.7.1.3.7)</td>
        </tr>
        <tr>
            <td>nav_modes</td>
            <td colspan=2>set of engaged automation modes: 'autopilot', 'vnav', 'althold', 'approach', 'lnav', 'tcas'</td>
        </tr>
        <tr>
            <td>lat</td>
            <td colspan=2>the aircraft position in decimal degrees</td>
        </tr>
        <tr>
            <td>lon</td>
            <td colspan=2>the aircraft position in decimal degrees</td>
        </tr>
        <tr>
            <td>nic</td>
            <td colspan=2>Navigation Integrity Category (2.2.3.2.7.2.6)</td>
        </tr>
        <tr>
            <td>rc</td>
            <td colspan=2>Radius of Containment, meters; a measure of position integrity derived from NIC & supplementary bits. (2.2.3.2.7.2.6, Table 2-69)</td>
        </tr>
        <tr>
            <td>seen_pos</td>
            <td colspan=2>how long ago (in seconds before "now") the position was last updated</td>
        </tr>
        <tr>
            <td>version</td>
            <td colspan=2>ADS-B Version Number 0, 1, 2 (3-7 are reserved) (2.2.3.2.7.5)</td>
        </tr>
        <tr>
            <td>nic_baro</td>
            <td colspan=2>Navigation Integrity Category for Barometric Altitude (2.2.5.1.35)</td>
        </tr>
        <tr>
            <td>nac_p</td>
            <td colspan=2>Navigation Accuracy for Position (2.2.5.1.35)</td>
        </tr>
        <tr>
            <td>nac_v</td>
            <td colspan=2>Navigation Accuracy for Velocity (2.2.5.1.19)</td>
        </tr>
        <tr>
            <td>sil</td>
            <td colspan=2>Source Integity Level (2.2.5.1.40)</td>
        </tr>
        <tr>
            <td>sil_type</td>
            <td colspan=2>interpretation of SIL: unknown, perhour, persample</td>
        </tr>
        <tr>
            <td>gva</td>
            <td colspan=2>Geometric Vertical Accuracy  (2.2.3.2.7.2.8)</td>
        </tr>
        <tr>
            <td>sda</td>
            <td colspan=2>System Design Assurance (2.2.3.2.7.2.4.6)</td>
        </tr>
        <tr>
            <td>mlat</td>
            <td colspan=2>list of fields derived from MLAT data</td>
        </tr>
        <tr>
            <td>tisb</td>
            <td colspan=2>list of fields derived from TIS-B data</td>
        </tr>
        <tr>
            <td>messages</td>
            <td colspan="2">Atotal number of Mode S messages received from this aircraft</td>
        </tr>
        <tr>
            <td>seen</td>
            <td colspan="2">Ahow long ago (in seconds before "now") a message was last received from this aircraft</td>
        </tr>
        <tr>
            <td>rssi</td>
            <td colspan="2">Arecent average RSSI (signal power), in dbFS; this will always be negative.</td>
        </tr>
    </tbody>
</table>