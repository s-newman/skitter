package skitter.auth;

public class SignUp {

    private String rit_username;
    private String firstname;
    private String lastname;

    public SignUp(String rit_username, String firstname, String lastname) {
        this.rit_username = rit_username;
        this.firstname = firstname;
        this.lastname = lastname;
    }

    public String getRit_username() {
        return rit_username;
    }

    public void setRit_username(String rit_username) {
        this.rit_username = rit_username;
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
