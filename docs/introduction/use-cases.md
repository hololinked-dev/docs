<table>
  <tr>
    <th>Protocol</th>
    <th>Plausible Use Cases</th>
    <th>Operations</th>
    <th>Underlying Implementation</th>
    <th>Security</th>
  </tr>
  <tr>
    <td>HTTP</td>
    <td>Web Apps</td>
    <td>
      Properties, <br/> Actions, <br/> Events
    </td>
    <td>
      <a href="https://github.com/tornadoweb/tornado">tornado</a>
    </td>
    <td>
      username-password, <br/>
      device API key, <br/>
      IP filter, <br/>
      OAuth2 OIDC
    </td>
  </tr>
  <tr>
    <td>ZMQ TCP</td>
    <td>Networked Control Systems, devices in protected networks, containerized apps like in Kubernetes</td>
    <td rowspan="3">
      Properties, <br/> Actions, <br/> Events
    </td>
    <td rowspan="3"><a href="https://github.com/zeromq/pyzmq">pyzmq</a></td>
    <td rowspan="2">
      planned, likely may take upto end of 2026, please use HTTP if needed. Its not slow. 
    </td>
  </tr>
  <tr>
    <td>ZMQ IPC</td>
    <td>Desktop Applications, Python Dashboards without exposing device API directly on network  (streamlit, dash, panel etc.)</td>
  </tr>
  <tr>
    <td>ZMQ INPROC</td>
    <td>
      High Speed Desktop Applications (again, not exposed on network), currently you will need some CPP magic or disable GIL to leverage it fully
    </td>
    <td>
      No security, meant for in-process communication only
    </td>
  </tr>
  <tr>
    <td>MQTT</td>
    <td>
      Reliable pub-sub & incorporating into existing systems that use MQTT for lightweight messaging
    </td>
    <td rowspan="2">
      Properties that emit change events, <br /> plain Events
    </td>
    <td rowspan="2">
      <a href="https://github.com/empicano/aiomqtt">aiomqtt</a>/<a href="https://www.eclipse.org/paho/">Eclipse Paho</a>
    </td>
    <td rowspan="2">
      username-password, <br/>
      TLS with client certificates (you set this up in the broker anyway)
    </td>
  </tr>
  <tr>
    <td>MQTT with websockets</td>
    <td>
      planned for April/May 2026 release.
    </td>
  </tr>
  <tr>
    <td>
      CoAP <br/>
      CoAP Websockets <br/>
      CoAP UDP
    </td>
    <td>
      Planned, April 2026.
    </td>
    <td>
      Will be updated 
    </td>
    <td>
      <a href="https://github.com/chrysn/aiocoap">aiocoap</a>
    </td>
    <td>
      Will be updated
    </td>
  </tr>
</table>
