package skitter.auth;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class DB {

    static final private String jdbcDriver = "com.mysql.jdbc.Driver";
    private String username = "root";
    private String password = "";
    private String URL = "jdbc:mysql://";
    private String DBName;
    private String DBHost;
    private Connection conn;

    public DB(String DBHost, String DBName) throws Exception {
        this.DBName = DBName;
        this.DBHost = DBHost;
        this.URL = this.URL + this.DBHost + "/" + this.DBName + "?autoReconnect=true&useSSL=false";
        this.conn = makeConnection();
        if (this.conn == null) {
            throw new SQLException();
        }
    }

    public Connection makeConnection() {
        Connection conn;
        try {
            Class.forName(jdbcDriver);
            conn = DriverManager.getConnection(URL, username, password);
        } catch (Exception e) {
            return null;
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
