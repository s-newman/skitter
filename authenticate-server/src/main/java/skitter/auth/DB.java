package skitter.auth;

import java.sql.Connection;
import java.sql.DriverManager;

public class DB {
    // TODO: Database credentials.
    static final private String jdbcDriver = "com.mysql.jdbc.Driver";
    private String username = "api-gateway";
    private String password = "changemeplease-securitysucks";
    private String URL = "jdbc:mysql://";
    private String DBName;
    private String DBHost;
    private Connection conn;

    public DB(String DBHost, String DBName) {
        this.DBName = DBName;
        this.DBHost = DBHost;
        this.URL = this.URL + this.DBHost + "/" + this.DBName + "?autoReconnect=true&useSSL=false";
        this.conn = makeConnection();
    }

    public Connection makeConnection() {
        Connection conn = null;

        // Continue to attempt to connect until a connection is established
        while(conn == null) {
            try {
                Class.forName(jdbcDriver);
                conn = DriverManager.getConnection(URL, username, password);
            } catch (Exception e) {
                System.out.println(e.getMessage());
            }
        }
        return conn;
    }

    public void destroyConnection() {
        if (this.conn != null) {
            try {
                this.conn.close();
            } catch (Exception e) {
                System.err.println(e.getMessage());
            }
        }
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public Connection getConn() {
        return conn;
    }
}
