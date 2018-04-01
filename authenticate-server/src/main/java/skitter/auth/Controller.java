package skitter.auth;

import org.json.simple.JSONObject;
import org.springframework.ldap.core.AttributesMapper;
import org.springframework.ldap.core.LdapTemplate;
import org.springframework.ldap.filter.AndFilter;
import org.springframework.ldap.filter.PresentFilter;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import javax.naming.NamingException;
import javax.naming.directory.Attributes;
import java.security.SecureRandom;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.List;

import static org.springframework.web.bind.annotation.RequestMethod.GET;
import static org.springframework.web.bind.annotation.RequestMethod.POST;

@RestController
public class Controller {
    // TODO: javadocs for the endpoints

    final private static String baseDn = "ou=People,dc=rit,dc=edu";
    final private static int tokenLength = 40;
    private DB db;

    public Controller() {
        try {
            String DBHost = "user-db";
            if (System.getenv("DBHOST") != null) {
                DBHost = System.getenv("DBHOST");
            }
            db = new DB(DBHost, "users");
            if (System.getenv("DBUSER") != null) {
                db.setUsername(System.getenv("DBUSER"));
            }
            if (System.getenv("DBPASS") != null) {
                db.setPassword(System.getenv("DBPASS"));
            }
        } catch (Exception e) {
            System.err.println(e.getMessage());
            System.exit(1);
        }
    }

    private static String generateSessionID() {
        SecureRandom rand = new SecureRandom();
        String token = "";
        for (int i = 0; i < tokenLength; i++) {
            token = token + Integer.toHexString(rand.nextInt(0x100));
        }
        return token;
    }

    @RequestMapping(value = "/signIn", method = POST, produces = "application/json")
    public String signIn(@RequestBody SignIn signin) {

        JSONObject response = new JSONObject();
        response.put("successful", "false");
        response.put("sessionID", "");
        response.put("message", "");

        String username = signin.getUsername();
        String password = signin.getPassword();

        LDAPConfiguration config = new LDAPConfiguration();
        config.setUsername("uid=" + username + "," + baseDn);
        config.setPassword(password);

        AndFilter filter = new AndFilter();
        filter.and(new PresentFilter("objectclass"));

        boolean authenticated;
        List<Person> people = null;

        // LDAP Auth
        try {
            LdapTemplate template = config.ldapTemplate();
            authenticated = template.authenticate("uid=" + username + "," + baseDn, filter.encode(), password);
            people = template.search("uid=" + username + "," + baseDn, filter.encode(), new PersonAttributesMapper());
        } catch (Exception e) {
            System.err.println(e.getMessage());
            response.replace("message", "Authentication error");
            return response.toJSONString();
        }

        // Successful LDAP Auth
        if (authenticated) {
            if (people == null) {
                response.replace("message", "Cannot get user information");
                return response.toJSONString();
            }

            PreparedStatement stmt = null;
            String sessionID = "";

            // Check if a session is already established.
            try {
                stmt = db.getConn().prepareStatement("SELECT * FROM SESSION WHERE rit_username = ?;");
                stmt.setString(1, username);
                ResultSet rs = stmt.executeQuery();
                rs.last();
                int nRow = rs.getRow();

                if (nRow == 1) {
                    sessionID = rs.getString("session_id");
                    rs.close();
                } else if (nRow != 0){
                    response.replace("message", "session information is corrupted");
                    return response.toJSONString();
                }
            } catch (Exception e) {
                System.err.println(e.getMessage());
                response.replace("message", "Error retrieving session information");
                return response.toJSONString();
            } finally {
                try {
                    if (stmt != null) {
                        stmt.close();
                    }
                } catch (Exception e) {
                    System.err.println(e.getMessage());
                    response.replace("message", "Cannot close statement");
                    return response.toJSONString();
                }
            }

            // Create new session
            if (sessionID.equals("")) {
                try {
                    stmt = db.getConn().prepareStatement("INSERT INTO SESSION (rit_username, session_id) VALUES (?, ?)");
                    stmt.setString(1, username);
                    sessionID = generateSessionID();
                    stmt.setString(2, sessionID);
                    stmt.executeUpdate();
                } catch (Exception e) {
                    System.err.println(e.getMessage());
                    response.replace("message", "Error creating session entry");
                    return response.toJSONString();
                } finally {
                    try {
                        if (stmt != null) {
                            stmt.close();
                        }
                    } catch (Exception e) {
                        System.err.println(e.getMessage());
                        response.replace("message", "Cannot close statement");
                        return response.toJSONString();
                    }
                }
            }

            response.replace("successful", "true");
            response.replace("sessionID", sessionID);
            JSONObject person = new JSONObject();
            person.put("lastname", people.get(0).getLastName());
            person.put("firstname", people.get(0).getFirstName());
            response.replace("message", person);
            return response.toJSONString();
        }

        response.replace("message", "unknown error");
        return response.toJSONString();
    }

    @RequestMapping(value = "/isAuthenticated", method = GET, produces = "application/json")
    public String isAuthenticated(@RequestParam("username") String username) {
        PreparedStatement stmt = null;
        JSONObject response = new JSONObject();
        response.put("authenticated", "false");
        response.put("message", "");

        try {
            stmt = db.getConn().prepareStatement("SELECT * FROM SESSION WHERE rit_username = ?;");
            stmt.setString(1, username);
            ResultSet rs = stmt.executeQuery();
            rs.last();
            int nRow = rs.getRow();
            if (nRow == 1) {
                response.replace("authenticated", "true");
            } else if (nRow != 0) {
                response.replace("message", "Unknown database error");
            }
            rs.close();
            return response.toJSONString();
        } catch (Exception e) {
            System.err.println(e.getMessage());
            response.replace("message", "Error executing SQL statement");
            return response.toJSONString();
        } finally {
            try {
                if (stmt != null) {
                    stmt.close();
                }
            } catch (Exception e) {
                System.err.println(e.getMessage());
                response.replace("message", "Cannot close statement");
                return response.toJSONString();
            }
        }
    }

    @RequestMapping(value = "/newUser", method = POST, produces = "application/json")
    public String newUser(@RequestBody SignUp signup) {
        String rit_username = signup.getRit_username();
        String username = signup.getUsername();
        String firstname = signup.getFirstname();
        String lastname = signup.getLastname();

        String email = rit_username + "@rit.edu";
        int profile_picture_id = 0;

        JSONObject response = new JSONObject();
        response.put("successful", "false");
        response.put("message", "");

        PreparedStatement stmt = null;

        // Check existing account
        try {
            stmt = db.getConn().prepareStatement("SELECT * FROM USER_INFO WHERE rit_username = ?;");
            stmt.setString(1, rit_username);
            ResultSet rs = stmt.executeQuery();
            rs.last();
            int nRow = rs.getRow();
            if (nRow == 1) {
                response.replace("message", "User already has an account");
                return response.toJSONString();
            } else if (nRow != 0) {
                response.replace("message", "User information corrupted. Please check the database");
                return response.toJSONString();
            }
        } catch (Exception e) {
            System.err.println(e.getMessage());
            response.replace("message", "Error retrieving user information: rit_username");
            return response.toJSONString();
        } finally {
            try {
                if (stmt != null) {
                    stmt.close();
                }
            } catch (Exception e) {
                System.err.println(e.getMessage());
                response.replace("message", "Cannot close statement");
                return response.toJSONString();
            }
        }

        // Check duplicated username
        try {
            stmt = db.getConn().prepareStatement("SELECT * FROM USER_INFO WHERE username = ?;");
            stmt.setString(1, username);
            ResultSet rs = stmt.executeQuery();
            rs.last();
            int nRow = rs.getRow();
            if (nRow == 1) {
                response.replace("message", "Username not available");
                return response.toJSONString();
            } else if (nRow != 0) {
                response.replace("message", "User information corrupted. Please check the database");
                return response.toJSONString();
            }
        } catch (Exception e) {
            System.err.println(e.getMessage());
            response.replace("message", "Error retrieving user information: username");
            return response.toJSONString();
        } finally {
            try {
                if (stmt != null) {
                    stmt.close();
                }
            } catch (Exception e) {
                System.err.println(e.getMessage());
                response.replace("message", "Cannot close statement");
                return response.toJSONString();
            }
        }

        // Make new user
        try {
            stmt = db.getConn().prepareStatement("INSERT INTO USER_INFO (username, rit_username, first_name, last_name, email, private_account, profile_picture_id) VALUES (?, ?, ?, ?, ?, ?, ?)");
            stmt.setString(1, username);
            stmt.setString(2, rit_username);
            stmt.setString(3, firstname);
            stmt.setString(4, lastname);
            stmt.setString(5, email);
            stmt.setBoolean(6, false);
            stmt.setInt(7, profile_picture_id);
            stmt.executeUpdate();
        } catch (Exception e) {
            System.err.println(e.getMessage());
            response.replace("message", "Error executing SQL statement");
            return response.toJSONString();
        } finally {
            try {
                if (stmt != null) {
                    stmt.close();
                }
            } catch (Exception e) {
                System.err.println(e.getMessage());
                response.replace("message", "Cannot close statement");
                return response.toJSONString();
            }
        }

        response.replace("successful", "true");
        return response.toJSONString();
    }

    /**
     * Delete a user from a database. At this point it's only for testing purpose.
     * @param rit_username: The RIT username of the account to be deleted
     * @return {
     *     successful: true if the user is successfully removed, false otherwise.
     *     messsage: any error message.
     * }
     */
    @RequestMapping(value = "/deleteUser", method = GET, produces = "application/json")
    public String deleteUser(@RequestParam("rit_username") String rit_username) {
        PreparedStatement stmt = null;
        JSONObject response = new JSONObject();
        response.put("successful", "false");
        response.put("message", "");

        try {
            stmt = db.getConn().prepareStatement("DELETE FROM USER_INFO WHERE rit_username = ?;");
            stmt.setString(1, rit_username);
            int nRow = stmt.executeUpdate();

            if (nRow == 1) {
                response.replace("successful", "true");
            } else if (nRow != 0) {
                response.replace("message", "Unknown database error");
            } else {
                response.replace("message", "User does not exists");
            }
            return response.toJSONString();
        } catch (Exception e) {
            System.err.println(e.getMessage());
            response.replace("message", "Error executing SQL statement");
            return response.toJSONString();
        } finally {
            try {
                if (stmt != null) {
                    stmt.close();
                }
            } catch (Exception e) {
                System.err.println(e.getMessage());
                response.replace("message", "Cannot close statement");
                return response.toJSONString();
            }
        }
    }

    private class PersonAttributesMapper implements AttributesMapper<Person> {
        public Person mapFromAttributes(Attributes attrs) throws NamingException {
            Person person = new Person();
            person.setLastName((String) attrs.get("sn").get());
            person.setFirstName((String) attrs.get("givenName").get());
            return person;
        }
    }

}
