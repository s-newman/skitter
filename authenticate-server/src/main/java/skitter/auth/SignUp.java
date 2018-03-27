package skitter.auth;

public class SignUp {

    private String rit_username;
    private String username;
    private String firstname;
    private String lastname;

    public SignUp(String rit_username, String username, String firstname, String lastname) {
        this.rit_username = rit_username;
        this.username = username;
        this.firstname = firstname;
        this.lastname = lastname;
    }

    public String getRit_username() {
        return rit_username;
    }

    public void setRit_username(String rit_username) {
        this.rit_username = rit_username;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getFirstname() {
        return firstname;
    }

    public void setFirstname(String firstname) {
        this.firstname = firstname;
    }

    public String getLastname() {
        return lastname;
    }

    public void setLastname(String lastname) {
        this.lastname = lastname;
    }
}
